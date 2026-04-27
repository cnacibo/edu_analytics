import './styles/MapDashboard.css';
import React, { useCallback, useMemo, useState, useRef, useEffect } from 'react';
import { YMaps, Map, Placemark, ZoomControl } from '@pbe/react-yandex-maps';
import LoadingSpinner from '../common/LoadingSpinner';
import Error from '../common/Error';
import { mapApi } from '../../api';

const MapDashboard = ({ avgCost }) => {
  const [loading, setLoading] = useState(true);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [error, setError] = useState(null);
  const [programs, setPrograms] = useState([]);
  const mapRef = useRef(null);

  const YANDEX_MAPS_API_KEY = process.env.REACT_APP_YANDEX_MAPS_API_KEY;

  useEffect(() => {
    fetchMapData();
  }, []);

  const fetchMapData = async () => {
    try {
      const bachelorResponse = await mapApi.getMapBachelorData();
      const masterResponse = await mapApi.getMapMasterData();

      const bachelorData = bachelorResponse.data.bachelor_programs_map || [];
      const masterData = masterResponse.data.master_programs_map || [];

      const transform = (list) =>
        list.map((item) => ({
          ...item,
          coords: [item.latitude, item.longitude],
        }));

      setPrograms([...transform(bachelorData), ...transform(masterData)]);
    } catch (error) {
      console.error('Error fetching programs for map:', error);
    }
  };

  const handleMapLoad = () => {
    setMapLoaded(true);
    setLoading(false);
    setError(null);
  };

  const handleMapError = (error) => {
    console.error('Ошибка карты:', error);
    setError(error?.message || 'Ошибка загрузки карты');
    setLoading(false);
  };

  const mapState = useMemo(
    () => ({
      center: [64.686, 80.745],
      zoom: 3,
      controls: [],
    }),
    []
  );

  const mapOptions = useMemo(
    () => ({
      suppressMapOpenBlock: true,
      yandexMapDisablePoiInteractivity: true,
    }),
    []
  );

  const getPlacemarkOptions = useCallback(
    (program) => {
      if (program.cost === null || program.cost === undefined) {
        return {
          iconColor: '#9e9e9e',
          preset: 'islands#grayIcon',
          hideIconOnBalloonOpen: false,
          balloonCloseButton: true,
        };
      }

      const isExpensive = program.cost > avgCost;
      return {
        iconColor: isExpensive ? '#f16a8c' : '#457b9d',
        preset: isExpensive ? 'islands#redDotIcon' : 'islands#blueDotIcon',
        hideIconOnBalloonOpen: false,
        balloonCloseButton: true,
      };
    },
    [avgCost]
  );

  const createBalloonContent = useCallback(
    (program) => {
      const costValue =
        program.cost !== null && program.cost !== undefined
          ? program.cost.toLocaleString()
          : 'не указана';
      const costClass =
        program.cost !== null && program.cost !== undefined
          ? program.cost > avgCost
            ? 'expensive'
            : 'cheap'
          : 'unknown';
      const costBadge =
        program.cost !== null && program.cost !== undefined
          ? program.cost > avgCost
            ? 'Дороже среднего'
            : 'Дешевле среднего'
          : 'Стоимость неизвестна';
      return `
      <div class="balloon-container">
        <h3 class="balloon-title ${costClass}">${program.name}</h3>
        <div class="balloon-details">
          <p class="balloon-detail-item">
            <span class="balloon-detail-label">📍 Город:</span>
            <span class="balloon-detail-value">${program.city}</span>
          </p>
          <p class="balloon-detail-item">
            <span class="balloon-detail-label">💰 Стоимость:</span>
            <span class="balloon-detail-value">${costValue} ₽/год</span>
          </p>
        </div>
        <div class="balloon-badge ${costClass}">
          ${costBadge}
        </div>
      </div>
    `;
    },
    [avgCost]
  );

  const handlePlacemarkClick = (program) => {
    if (mapRef.current) {
      mapRef.current.balloon.open(program.coords, {
        contentBody: createBalloonContent(program),
      });
    }
  };

  return (
    <YMaps
      query={{ apikey: YANDEX_MAPS_API_KEY, lang: 'ru_RU' }}
      onError={(error) => {
        console.error('YMaps ошибка:', error);
        setError('Ошибка загрузки карт');
        setLoading(false);
      }}
    >
      <div className="yandex-map-container">
        <div style={{ opacity: mapLoaded ? 1 : 0, transition: 'opacity 0.5s' }}>
          <Map
            instanceRef={mapRef}
            state={mapState}
            width="100%"
            height="500px"
            options={mapOptions}
            onLoad={handleMapLoad}
            onError={handleMapError}
          >
            <ZoomControl options={{ float: 'right' }} />

            {programs.map((program) => (
              <Placemark
                key={program.id}
                geometry={program.coords}
                options={getPlacemarkOptions(program)}
                properties={{
                  hintContent: program.name,
                }}
                onClick={() => handlePlacemarkClick(program)}
              />
            ))}
          </Map>
        </div>

        {loading && (
          <div className="map-overlay">
            <LoadingSpinner input="карты" />
          </div>
        )}
        {error && !loading && (
          <div className="map-overlay">
            <Error message={error} />
          </div>
        )}
        {mapLoaded && (
          <div className="map-legend">
            <div className="legend-title">Условные обозначения</div>
            <div className="legend-item">
              <span className="legend-marker expensive-marker"></span>
              <span>Дороже среднего</span>
            </div>
            <div className="legend-item">
              <span className="legend-marker cheap-marker"></span>
              <span>Дешевле среднего</span>
            </div>
          </div>
        )}
      </div>
    </YMaps>
  );
};

export default MapDashboard;
