import './styles/KnowledgeGraphPage.css';
import Plot from 'react-plotly.js';
import React, { useEffect, useMemo, useState } from 'react';
import { graphApi } from '../api';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Error from '../components/common/Error';

const TYPE_COLORS = {
  direction: '#f39cbb',
  subject: '#457b9d',
  tag: '#cbeef3',
  default: '#999',
};

const KnowledgeGraphPage = () => {
  const [graph, setGraph] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [activeTypes, setActiveTypes] = useState({
    direction: true,
    subject: true,
    tag: false,
  });
  const [minDegree, setMinDegree] = useState(0);

  useEffect(() => {
    fetchGraphData();
  }, []);

  const fetchGraphData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await graphApi.getGraphData();
      setGraph(response);
    } catch (err) {
      console.error('Error fetching graph:', err);
      setError(err.message || 'Ошибка загрузки');
    } finally {
      setLoading(false);
    }
  };

  const nodeDegreeMap = useMemo(() => {
    if (!graph || !graph.nodes || !graph.edges) return {};
    const map = {};
    graph.nodes.forEach((n) => (map[n.label] = 0));
    graph.edges.forEach((e) => {
      if (map[e.source] !== undefined) map[e.source] += 1;
      if (map[e.target] !== undefined) map[e.target] += 1;
    });
    return map;
  }, [graph]);

  const { nodesTrace, edgeShapes } = useMemo(() => {
    if (!graph || !graph.nodes || !graph.nodes.length) return { nodesTrace: null, edgeShapes: [] };

    const filteredNodes = graph.nodes.filter((n) => {
      const typeOk = activeTypes[n.type] === true;
      const degreeOk = (nodeDegreeMap[n.label] || 0) >= minDegree;
      return typeOk && degreeOk;
    });

    const visibleLabels = new Set(filteredNodes.map((n) => n.label));

    const nodesTrace = {
      x: filteredNodes.map((n) => n.x),
      y: filteredNodes.map((n) => n.y),
      text: filteredNodes.map((n) => n.label),
      type: 'scatter',
      mode: 'markers+text',
      textposition: 'top center',
      hoverinfo: 'text',
      textfont: { size: 10, color: '#333' },
      marker: {
        size: 14,
        color: filteredNodes.map((n) => TYPE_COLORS[n.type] || TYPE_COLORS.default),
        line: { width: 1, color: '#fff' },
      },
      name: '',
      showlegend: false,
    };

    const nodeMap = {};
    filteredNodes.forEach((n) => {
      nodeMap[n.label] = { x: n.x, y: n.y };
    });

    const edgeShapes = (graph.edges || [])
      .filter((e) => nodeMap[e.source] && nodeMap[e.target])
      .map((e) => ({
        type: 'line',
        xref: 'x',
        yref: 'y',
        x0: nodeMap[e.source].x,
        y0: nodeMap[e.source].y,
        x1: nodeMap[e.target].x,
        y1: nodeMap[e.target].y,
        line: { color: '#d0d0d0', width: 0.8 },
      }));

    return { nodesTrace, edgeShapes };
  }, [graph, activeTypes, minDegree, nodeDegreeMap]);

  const plotLayout = useMemo(
    () => ({
      title: 'Граф знаний',
      showlegend: false,
      hovermode: 'closest',
      xaxis: { visible: false, showgrid: false, zeroline: false },
      yaxis: { visible: false, showgrid: false, zeroline: false },
      margin: { l: 0, r: 0, t: 40, b: 0 },
      paper_bgcolor: 'white',
      plot_bgcolor: 'white',
      shapes: edgeShapes,
    }),
    [edgeShapes]
  );

  const handleTypeToggle = (type) => {
    setActiveTypes((prev) => ({ ...prev, [type]: !prev[type] }));
  };

  if (loading) return <LoadingSpinner input="графа" />;
  if (error || !graph || !graph.nodes || graph.nodes.length === 0)
    return <Error onRetry={fetchGraphData} message="Не удалось загрузить данные графа" />;

  return (
    <div className="knowledge-graph-page">
      <div className="filter-panel">
        <div>
          <strong>Тип узла:</strong>
          {['direction', 'subject', 'tag'].map((type) => (
            <label key={type} className="filter-label">
              <input
                type="checkbox"
                checked={activeTypes[type] || false}
                onChange={() => handleTypeToggle(type)}
              />
              <span style={{ color: TYPE_COLORS[type] }}>● {type}</span>
            </label>
          ))}
        </div>
        <div>
          <label>
            <strong>Мин. связей:</strong>
          </label>
          <input
            type="number"
            min={0}
            value={minDegree}
            onChange={(e) => setMinDegree(parseInt(e.target.value, 10) || 0)}
            style={{ marginLeft: 8, width: 60 }}
          />
        </div>
      </div>

      <div className="graph-area">
        <Plot
          data={[nodesTrace]}
          layout={plotLayout}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: '100%', height: '100%' }}
          useResizeHandler={true}
        />
      </div>
    </div>
  );
};

export default KnowledgeGraphPage;
