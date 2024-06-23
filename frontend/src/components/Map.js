import mapboxgl from 'mapbox-gl';
import React, { useEffect, useRef, useState } from 'react';
import { useSelector } from 'react-redux';
import { createRoot } from 'react-dom/client';
import emergencyData from '../static/berkeleyEmergencyResponse.json';

import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiYmxhaXJvcmNoYXJkIiwiYSI6ImNsNWZzeGtrNDEybnMzaXA4eHRuOGU5NDUifQ.s59N5x1EqfyPZxeImzNwbw';
console.log(emergencyData);

const Marker = ({ onClick, children, call }) => {
  const _onClick = () => {
    onClick(call);
  };

  return (
    <button onClick={_onClick} className="marker">
      {children}
    </button>
  );
};

const Map = () => {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const markersRef = useRef({});
  const animationRef = useRef(null);
  const calls = useSelector(state => state.calls);
  const [geocoder, setGeocoder] = useState(null);
  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/dark-v11',
      center: [-122.272747, 37.871853],
      zoom: 12,
      pitch: 60,
      bearing: -60,
      antialias: true,
      attributionControl: false
    });

    mapRef.current = map;

    map.on('style.load', () => {
      map.addSource('emergency-locations', {
        type: 'geojson',
        data: emergencyData
      });

      // Add a layer for fire stations
      map.addLayer({
        id: 'fire-stations',
        type: 'circle',
        source: 'emergency-locations',
        filter: ['==', ['get', 'type'], 'Fire Station'],
        paint: {
          'circle-radius': 10,
          'circle-color': 'purple',
          'circle-opacity': 0.6,
          'circle-stroke-width': 2,
          'circle-stroke-color': 'white'
        }
      });

      // Add a layer for police stations
      map.addLayer({
        id: 'police-stations',
        type: 'circle',
        source: 'emergency-locations',
        filter: ['==', ['get', 'type'], 'Police Station'],
        paint: {
          'circle-radius': 10,
          'circle-color': 'blue',
          'circle-opacity': 0.6,
          'circle-stroke-width': 2,
          'circle-stroke-color': 'white'
        }
      });
      
      map.addSource('mapbox-dem', {
        'type': 'raster-dem',
        'url': 'mapbox://mapbox.mapbox-terrain-dem-v1',
        'tileSize': 512,
        'maxzoom': 14
      });
      map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.5 });

      map.addLayer({
        'id': 'sky',
        'type': 'sky',
        'paint': {
          'sky-type': 'atmosphere',
          'sky-atmosphere-sun': [0.0, 90.0],
          'sky-atmosphere-sun-intensity': 15
        }
      });
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-right');

    // Initialize geocoder
    const mbxGeocoding = require('@mapbox/mapbox-sdk/services/geocoding');
    const geocodingClient = mbxGeocoding({ accessToken: mapboxgl.accessToken });
    setGeocoder(geocodingClient);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      map.remove();
    };
  }, []);

  useEffect(() => {
    if (!geocoder || !mapRef.current) return;

    const newMarkers = [];

    // Update markers for each call
    const updateMarkers = async () => {
      for (const call of calls) {
        if (!call.location) continue;

        try {
          const response = await geocoder.forwardGeocode({
            query: call.location,
            limit: 1
          }).send();

          if (response && response.body && response.body.features && response.body.features.length) {
            const [lng, lat] = response.body.features[0].center;
            
            if (markersRef.current[call.id]) {
              // Update existing marker
              markersRef.current[call.id].setLngLat([lng, lat]);
            } else {
              // Create new marker
              const markerNode = document.createElement('div');
              const root = createRoot(markerNode);
              root.render(<Marker onClick={markerClicked} call={call} />);

              const marker = new mapboxgl.Marker(markerNode)
                .setLngLat([lng, lat])
                .addTo(mapRef.current);

              markersRef.current[call.id] = marker;
            }
            newMarkers.push({ id: call.id, lngLat: [lng, lat] });
          }
        } catch (error) {
          console.error('Error geocoding location:', error);
        }
      }

      // Remove markers for calls that no longer exist
      Object.keys(markersRef.current).forEach(id => {
        if (!calls.find(call => call.id === id)) {
          markersRef.current[id].remove();
          delete markersRef.current[id];
        }
      });

      setMarkers(newMarkers);
    };

    updateMarkers();
  }, [calls, geocoder]);

  useEffect(() => {
    if (markers.length === 0 || !mapRef.current) return;

    let currentIndex = 0;
    const animateCamera = () => {
      const marker = markers[currentIndex];
      mapRef.current.easeTo({
        center: marker.lngLat,
        zoom: 15,
        duration: 3000,
        pitch: 60,
        bearing: (currentIndex * 45) % 360
      });

      currentIndex = (currentIndex + 1) % markers.length;
      
      // Schedule the next animation
      animationRef.current = setTimeout(() => {
        requestAnimationFrame(animateCamera);
      }, 6000); // 3 seconds for animation + 3 seconds pause
    };

    animateCamera();

    return () => {
      if (animationRef.current) {
        clearTimeout(animationRef.current);
      }
    };
  }, [markers]);

  const markerClicked = (call) => {
    // Handle marker click (e.g., show call details)
    console.log('Call clicked:', call);
  };

  return <div className="map-container" ref={mapContainerRef} />;
};

export default Map;