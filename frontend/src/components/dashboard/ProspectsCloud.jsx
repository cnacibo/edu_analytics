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
      const words = Object.entries(rawData).map(([text, value]) => ({ text, value }));
      setWords(words);
    } catch (error) {
      setError(error.message);
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const fontSizeMapper = (word) => Math.log2(word.value) * 20;

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
        width={500}
        height={300}
        font="Impact"
        fontSizeMapper={fontSizeMapper}
        rotate={() => 0}
        padding={5}
      />
    </div>
  );
};
export default ProspectsCloud;
