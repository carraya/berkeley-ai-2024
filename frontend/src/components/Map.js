import mapboxgl from 'mapbox-gl';
import React, { useEffect, useRef, useState } from 'react';
import { useSelector } from 'react-redux';
import { createRoot } from 'react-dom/client';
import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiYmxhaXJvcmNoYXJkIiwiYSI6ImNsNWZzeGtrNDEybnMzaXA4eHRuOGU5NDUifQ.s59N5x1EqfyPZxeImzNwbw';

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
  const calls = useSelector(state => state.calls);
  const [geocoder, setGeocoder] = useState(null);

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

    return () => map.remove();
  }, []);

  useEffect(() => {
    if (!geocoder) return;

    // Update markers for each call
    calls.forEach(async (call) => {
      if (!call.location) return;

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
        }
      } catch (error) {
        console.error('Error geocoding location:', error);
      }
    });

    // Remove markers for calls that no longer exist
    Object.keys(markersRef.current).forEach(id => {
      if (!calls.find(call => call.id === id)) {
        markersRef.current[id].remove();
        delete markersRef.current[id];
      }
    });
  }, [calls, geocoder]);

  const markerClicked = (call) => {
    // Handle marker click (e.g., show call details)
    console.log('Call clicked:', call);
  };

  return <div className="map-container" ref={mapContainerRef} />;
};

export default Map;