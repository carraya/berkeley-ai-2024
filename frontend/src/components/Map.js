import mapboxgl from 'mapbox-gl';
import React, { useEffect, useRef, useState } from 'react';
import { useSelector } from 'react-redux';
import { createRoot } from 'react-dom/client';
import emergencyData from '../static/berkeleyEmergencyResponse.json';
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
          'circle-color': 'red',
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
      map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 2 });

      map.addLayer({
        'id': 'sky',
        'type': 'sky',
        'paint': {
          'sky-type': 'atmosphere',
          'sky-atmosphere-sun': [0.0, 90.0],
          'sky-atmosphere-sun-intensity': 15
        }
      });

       // Add 3D buildings
       const layers = map.getStyle().layers;
       const labelLayerId = layers.find(
         (layer) => layer.type === 'symbol' && layer.layout['text-field']
       ).id;
       
       map.addLayer(
         {
           'id': '3d-buildings',
           'source': 'composite',
           'source-layer': 'building',
           'filter': ['==', 'extrude', 'true'],
           'type': 'fill-extrusion',
           'paint': {
             'fill-extrusion-color': '#313131',
             'fill-extrusion-height': [
               'interpolate',
               ['linear'],
               ['zoom'],
               0,
               0,
               8,
               ['*', ['get', 'height'], 0.1],
               12,
               ['*', ['get', 'height'], 0.5],
               16,
               ['get', 'height']
             ],
             'fill-extrusion-base': [
               'interpolate',
               ['linear'],
               ['zoom'],
               0,
               0,
               8,
               ['*', ['get', 'min_height'], 0.1],
               12,
               ['*', ['get', 'min_height'], 0.5],
               16,
               ['get', 'min_height']
             ],
             'fill-extrusion-opacity': [
               'interpolate',
               ['linear'],
               ['zoom'],
               0,
               0,
               8,
               0.3,
               12,
               0.7,
               16,
               0.9
             ]
           }
         },
         labelLayerId
       );
    });

    // map.addControl(new mapboxgl.NavigationControl(), 'top-right');

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

    const getNearestStation = (type, callLocation) => {
      const stations = emergencyData.features.filter(feature => feature.properties.type === type);
      let nearestStation = null;
      let minDistance = Infinity;

      stations.forEach(station => {
        const [stationLng, stationLat] = station.geometry.coordinates;
        const distance = Math.sqrt(
          Math.pow(callLocation[0] - stationLng, 2) + Math.pow(callLocation[1] - stationLat, 2)
        );
        if (distance < minDistance) {
          minDistance = distance;
          nearestStation = station.geometry.coordinates;
        }
      });

      return nearestStation;
    };

    const getRoute = async (start, end, layerId, lineColor) => {
      const query = await fetch(
        `https://api.mapbox.com/directions/v5/mapbox/driving/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
        { method: 'GET' }
      );
      const json = await query.json();
      const data = json.routes[0];
      const route = data.geometry.coordinates;
      const geojson = {
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'LineString',
          coordinates: route
        }
      };

      if (mapRef.current.getSource(layerId)) {
        mapRef.current.getSource(layerId).setData(geojson);
      } else {
        mapRef.current.addLayer({
          id: layerId,
          type: 'line',
          source: {
            type: 'geojson',
            data: geojson
          },
          layout: {
            'line-join': 'round',
            'line-cap': 'round'
          },
          paint: {
            'line-color': lineColor,
            'line-width': 5,
            'line-opacity': 0.75
          }
        });
      }
    };

    const updateMarkers = async () => {
      for (const call of calls) {
        if (!call.location) continue;

        //make sure callStatus is active
        if (call.callStatus !== "active") continue;

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

            const callLocation = [lng, lat];

            if (call.dispatchInformation && call.dispatchInformation.fire) {
              const nearestFireStation = getNearestStation('Fire Station', callLocation);
              if (nearestFireStation) {
                getRoute(nearestFireStation, callLocation, `fire-route-${call.id}`, 'red');
              }
            }

            if (call.dispatchInformation && call.dispatchInformation.police) {
              const nearestPoliceStation = getNearestStation('Police Station', callLocation);
              if (nearestPoliceStation) {
                getRoute(nearestPoliceStation, callLocation, `police-route-${call.id}`, 'blue');
              }
            }
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
        zoom: 16,
        duration: 3000,
        pitch: 60,
        bearing: (currentIndex * 45) % 360
      });

      currentIndex = (currentIndex + 1) % markers.length;

      // Schedule the next animation
      animationRef.current = setTimeout(animateCamera, 5000);
    };

    // Start the animation loop
    animateCamera();

    // Clean up on component unmount
    return () => {
      if (animationRef.current) {
        clearTimeout(animationRef.current);
      }
    };
  }, [markers]);

  const markerClicked = call => {
    console.log('Marker clicked:', call);
  };

  return <div ref={mapContainerRef} className="map-container" />;
};

export default Map;
