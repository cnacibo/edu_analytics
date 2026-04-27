import React, { useEffect, useState } from 'react';
import WordCloud from 'react-d3-cloud';
import { prospectsApi } from '../../api';
import LoadingSpinner from '../common/LoadingSpinner';
import Error from '../common/Error';

const ProspectsCloud = () => {
  const [words, setWords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCloudData();
  }, []);

  const fetchCloudData = async () => {
    setLoading(true);
    setError(null);
    try {
      const cloudDataResponse = await prospectsApi.getProspectsCloudData();
      const rawData = cloudDataResponse.data.wordcloud_data;
      const wordArray = Object.entries(rawData).map(([text, value]) => ({ text, value }));
      setWords(wordArray);
    } catch (error) {
      setError(error.message);
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const values = words.map((w) => w.value);
  const min = Math.min(...values);
  const max = Math.max(...values);

  const fontSize = (word) => {
    const normalized = (word.value - min) / (max - min);
    return 12 + Math.pow(normalized, 1.5) * 60;
  };

  const colors = [
    '#f39cbb',
    '#f16a8c',
    '#870e1d',
    '#dd2d4a',
    '#457b9d',
    '#90DDF0',
    '#80CFA9',
    '#F6CA83',
    '#4059AD',
    '#89BBFE',
    '#07393C',
    '#2C666E',
  ];

  if (loading) {
    return <LoadingSpinner input=""></LoadingSpinner>;
  }

  if (error || words.length === 0) {
    return <Error onRetry={fetchCloudData} message="Не удалось загрузить данные"></Error>;
  }

  return (
    <div className="prospects-cloud-container">
      <WordCloud
        data={words}
        width={600}
        height={450}
        font="Impact"
        fontWeight="bold"
        fontSize={fontSize}
        rotate={() => (Math.random() > 0.8 ? 90 : 0)}
        padding={1}
        fill={(word, index) => colors[index % colors.length]}
      />
    </div>
  );
};
export default ProspectsCloud;
