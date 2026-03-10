import './styles/SortedProgramsList.css';

const SortedProgramsList = () => {
  const topPrograms = [
    {
      id: 1,
      name: 'Программная инженерия',
      sphere: 'IT',
      level: 'Магистратура',
      university: 'ВШЭ',
      cost: 700000,
      score: 285,
    },
    {
      id: 2,
      name: 'Искусственный интеллект',
      sphere: 'IT',
      level: 'Бакалавриат',
      university: 'МФТИ',
      cost: 680000,
      score: 290,
    },
    {
      id: 3,
      name: 'Нефтегазовое дело',
      sphere: 'Инженерия',
      level: 'Специалитет',
      university: 'РГУ нефти и газа',
      cost: 650000,
      score: 260,
    },
    {
      id: 4,
      name: 'Лечебное дело',
      sphere: 'Медицина',
      level: 'Специалитет',
      university: 'Сеченовский университет',
      cost: 630000,
      score: 295,
    },
    {
      id: 5,
      name: 'Прикладная математика',
      sphere: 'Наука',
      level: 'Магистратура',
      university: 'МГУ',
      cost: 620000,
      score: 275,
    },
    {
      id: 6,
      name: 'Международный бизнес',
      sphere: 'Экономика',
      level: 'Магистратура',
      university: 'РАНХиГС',
      cost: 600000,
      score: 265,
    },
    {
      id: 7,
      name: 'Информационная безопасность',
      sphere: 'IT',
      level: 'Специалитет',
      university: 'Бауманка',
      cost: 590000,
      score: 270,
    },
    {
      id: 8,
      name: 'Биотехнологии',
      sphere: 'Наука',
      level: 'Магистратура',
      university: 'СПбГУ',
      cost: 580000,
      score: 255,
    },
    {
      id: 9,
      name: 'Архитектура',
      sphere: 'Творческие',
      level: 'Специалитет',
      university: 'МАРХИ',
      cost: 570000,
      score: 245,
    },
    {
      id: 10,
      name: 'Политология',
      sphere: 'Гуманитарные',
      level: 'Бакалавриат',
      university: 'МГИМО',
      cost: 560000,
      score: 260,
    },
  ];
  const getLevelColor = (level) => {
    const colors = {
      Специалитет: {
        background: '#f39dbc',
        text: 'black',
      },
      Бакалавриат: {
        background: '#cceff1',
        text: 'black',
      },
      Магистратура: {
        background: '#880d1f',
        text: 'white',
      },
    };
    return (
      colors[level] || {
        background: '#6c757d',
        text: 'white',
      }
    );
  };

  return (
    <div className="top-programs-container">
      <div className="top-programs-list">
        {topPrograms.map((program, index) => (
          <div key={program.id} className="top-program-item">
            <div className="top-program-rank">
              <span className={`top-rank-badge top-rank-${index + 1}`}>{index + 1}</span>
            </div>

            <div className="top-program-info">
              <div className="top-program-header">
                <h4 className="top-program-name">{program.name}</h4>
              </div>

              <div className="top-program-details">
                <div className="top-main-details">
                  <span className="top-program-cost">{program.cost.toLocaleString()} ₽</span>
                </div>
                <div className="top-extra-details">
                  <span className="top-program-score">Баллы: {program.score}</span>
                  <span
                    className="top-program-level"
                    style={{
                      backgroundColor: getLevelColor(program.level).background,
                      color: getLevelColor(program.level).text,
                    }}
                  >
                    {program.level}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="top-programs-footer">
        <span className="top-total-count">Всего программ: 8,526</span>
        <span className="top-avg-cost">
          Средняя стоимость в топ-10:{' '}
          {Math.round(
            topPrograms.reduce((sum, p) => sum + p.cost, 0) / topPrograms.length
          ).toLocaleString()}{' '}
          ₽
        </span>
      </div>
    </div>
  );
};

export default SortedProgramsList;
