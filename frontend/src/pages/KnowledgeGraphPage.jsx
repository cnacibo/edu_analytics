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

  useEffect(() => {
    fetchGraphData();
  }, []);

  const fetchGraphData = async () => {
    setLoading(true);
    setError(null);
    setGraph([]);
    try {
      const response = await graphApi.getGraphData();

      setGraph(response);
    } catch (error) {
      console.error('Error fetching graph:', error);
    } finally {
      setLoading(false);
    }
  };

  const { nodesTrace, edgeShapes } = useMemo(() => {
    if (!graph || !graph.nodes || !graph.nodes.length) return { nodesTrace: null, edgeShapes: [] };

    const nodesTrace = {
      x: graph.nodes.map((n) => n.x),
      y: graph.nodes.map((n) => n.y),
      text: graph.nodes.map((n) => n.label),
      type: 'scatter',
      mode: 'markers+text',
      textposition: 'top center',
      hoverinfo: 'text',
      textfont: { size: 10, color: '#333' },
      marker: {
        size: 14,
        color: graph.nodes.map((n) => TYPE_COLORS[n.type] || TYPE_COLORS.default),
        line: { width: 1, color: '#fff' },
      },
      name: '',
      showlegend: false,
    };

    const nodeMap = {};
    graph.nodes.forEach((n) => {
      nodeMap[n.label] = { x: n.x, y: n.y };
    });

    const edgeShapes = (graph.edges || [])
      .filter((e) => nodeMap[e.source] && nodeMap[e.target])
      .map((e, idx) => ({
        type: 'line',
        xref: 'x',
        yref: 'y',
        x0: nodeMap[e.source].x,
        y0: nodeMap[e.source].y,
        x1: nodeMap[e.target].x,
        y1: nodeMap[e.target].y,
        line: {
          color: '#d0d0d0',
          width: 0.8,
        },
      }));

    return { nodesTrace, edgeShapes };
  }, [graph]);

  const plotLayout = useMemo(() => {
    return {
      title: 'Граф знаний',
      showlegend: false,
      hovermode: 'closest',
      xaxis: { visible: false, showgrid: false, zeroline: false },
      yaxis: { visible: false, showgrid: false, zeroline: false },
      margin: { l: 0, r: 0, t: 40, b: 0 },
      paper_bgcolor: 'white',
      plot_bgcolor: 'white',
      shapes: edgeShapes,
    };
  }, [edgeShapes]);

  if (loading) {
    return <LoadingSpinner input="графа"></LoadingSpinner>;
  }

  if (error || graph.length === 0) {
    return <Error onRetry={fetchGraphData} message="Не удалось загрузить данные графа"></Error>;
  }

  return (
    <div className="knowledge-graph-container" style={{ height: '80vh' }}>
      <Plot
        data={[nodesTrace]}
        layout={plotLayout}
        config={{ responsive: true, displayModeBar: false }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />
    </div>
  );
};

export default KnowledgeGraphPage;
