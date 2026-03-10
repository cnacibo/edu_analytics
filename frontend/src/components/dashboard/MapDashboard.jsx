import './styles/MapDashboard.css';
import React, { useCallback, useMemo, useState, useRef } from 'react';
import { YMaps, Map, Placemark, ZoomControl } from '@pbe/react-yandex-maps';
import LoadingSpinner from '../common/LoadingSpinner';
import Error from '../common/Error';

const programs = [
  {
    id: 1,
    name: 'МГУ им. Ломоносова',
    city: 'Москва',
    coords: [55.703, 37.528],
    cost: 420000,
  },
  {
    id: 2,
    name: 'МГТУ им. Баумана',
    city: 'Москва',
    coords: [57.766, 37.683],
    cost: 380000,
  },
  {
    id: 3,
    name: 'СПбГУ',
    city: 'Санкт-Петербург',
    coords: [59.941, 30.298],
    cost: 400000,
  },
  {
    id: 4,
    name: 'НГУ',
    city: 'Новосибирск',
    coords: [54.843, 83.094],
    cost: 320000,
  },
  {
    id: 5,
    name: 'КФУ',
    city: 'Казань',
    coords: [55.79, 49.121],
    cost: 330000,
  },
  {
    id: 6,
    name: 'УрФУ',
    city: 'Екатеринбург',
    coords: [56.844, 60.652],
    cost: 310000,
  },
];

const AVG_COST = 390000;

const MapDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [error, setError] = useState(null);
  const mapRef = useRef(null);

  const YANDEX_MAPS_API_KEY = process.env.REACT_APP_YANDEX_MAPS_API_KEY;

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
    (cost) => ({
      iconColor: cost > AVG_COST ? '#f16a8c' : '#457b9d',
      preset: cost > AVG_COST ? 'islands#redDotIcon' : 'islands#blueDotIcon',
      hideIconOnBalloonOpen: false,
      balloonCloseButton: true,
      modules: ['balloon', 'hint'],
    }),
    []
  );

  const createBalloonContent = useCallback((program) => {
    const costClass = program.cost > AVG_COST ? 'expensive' : 'cheap';
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
          <span class="balloon-detail-value">${program.cost.toLocaleString()} ₽/год</span>
        </p>
      </div>
      <div class="balloon-badge ${costClass}">
        ${program.cost > AVG_COST ? 'Дороже среднего' : 'Дешевле среднего'}
      </div>
    </div>
  `;
  }, []);

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
                options={getPlacemarkOptions(program.cost)}
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
