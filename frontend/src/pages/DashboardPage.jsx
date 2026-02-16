import "./styles/DashboardPage.css"

const DashboardPage = () => {

    const stats = {
        totalPrograms: 8526,
        hsePrograms: 262,
        vuzPrograms: 8264,
        avgCost: 550000,
        sources: {
            hse: 262,
            vuz: 8264
        },
        avgCostByType: {
            bachelor: 520000,
            master: 620000,
            specialist: 580000
        },

        avgCostByFaculty: {
            it: 650000,
            economics: 480000,
            humanities: 420000,
            engineering: 590000,
            science: 540000
        },
        programLevels: {
            bachelor: 5230,
            master: 2840,
            specialist: 456
        },
        seats: {
            hse: {
                budget: 2840,
                paid: 1650,
                foreign: 420
            },
            vuz: {
                budget: 12450,
                paid: 45680,
                foreign: 2340
            },
            byYear: [
                { year: 1, budget: 3200, paid: 8900, foreign: 480 },
                { year: 2, budget: 3100, paid: 8700, foreign: 460 },
                { year: 3, budget: 3000, paid: 8500, foreign: 440 },
                { year: 4, budget: 2900, paid: 8300, foreign: 420 }
            ]
        },
        spheres: {
            it: 2134,
            economics: 1876,
            humanities: 1643,
            engineering: 1542,
            science: 1331
        },
        careerPaths: [
            { name: "IT и разработка", programs: 2456, avgSalary: 180000 },
            { name: "Управление и бизнес", programs: 1876, avgSalary: 150000 },
            { name: "Наука и образование", programs: 1432, avgSalary: 90000 },
            { name: "Инженерия", programs: 1234, avgSalary: 130000 },
            { name: "Медицина", programs: 876, avgSalary: 120000 },
            { name: "Творческие профессии", programs: 652, avgSalary: 85000 }
        ]
    }
return (
    <div className="dashboard-page">
        <div className="stats-grid">
            <div className="stat-card total-programs">
                    <div className="stat-content">
                        <span className="stat-label">Всего программ</span>
                        <span className="stat-value">{stats.totalPrograms.toLocaleString()}</span>
                    </div>
                </div>

                <div className="stat-card hse-programs">
                    <div className="stat-content">
                        <span className="stat-label">НИУ ВШЭ</span>
                        <span className="stat-value">{stats.hsePrograms.toLocaleString()}</span>
                    </div>
                </div>

            <div className="stat-card vuz-programs">
                    <div className="stat-content">
                        <span className="stat-label">Vuzopedia</span>
                        <span className="stat-value">{stats.vuzPrograms.toLocaleString()}</span>
                    </div>
            </div>
            <div className="stat-card avg-cost">
                    <div className="stat-content">
                        <span className="stat-label">Средняя стоимость</span>
                        <span className="stat-value">
                                    {stats.avgCost.toLocaleString()} ₽
                                </span>
                    </div>
            </div>
        </div>
        <div className="metrics-row">
            <div className="metrics-card">
                            <h3 className="metrics-title">Распределение по уровням образования</h3>
                            <div className="level-distribution">
                                <div className="level-item">
                                    <span className="level-label">Бакалавриат</span>
                                    <div className="level-bar">
                                        <div
                                            className="level-fill bachelor"
                                            style={{ width: `${(stats.programLevels.bachelor / stats.totalPrograms) * 100}%` }}
                                        ></div>
                                    </div>
                                    <span className="level-value">{stats.programLevels.bachelor.toLocaleString()}</span>
                                </div>
                                <div className="level-item">
                                    <span className="level-label">Магистратура</span>
                                    <div className="level-bar">
                                        <div
                                            className="level-fill master"
                                            style={{ width: `${(stats.programLevels.master / stats.totalPrograms) * 100}%` }}
                                        ></div>
                                    </div>
                                    <span className="level-value">{stats.programLevels.master.toLocaleString()}</span>
                                </div>
                                <div className="level-item">
                                    <span className="level-label">Специалитет</span>
                                    <div className="level-bar">
                                        <div
                                            className="level-fill specialist"
                                            style={{ width: `${(stats.programLevels.specialist / stats.totalPrograms) * 100}%` }}
                                        ></div>
                                    </div>
                                    <span className="level-value">{stats.programLevels.specialist.toLocaleString()}</span>
                                </div>
                            </div>
                        </div>

                        <div className="metrics-card">
                            <h3 className="metrics-title">Средняя стоимость по типам</h3>
                            <div className="cost-distribution">
                                <div className="cost-item">
                                    <span className="cost-label">Бакалавриат</span>
                                    <span className="cost-value">{stats.avgCostByType.bachelor.toLocaleString()} ₽</span>
                                </div>
                                <div className="cost-item">
                                    <span className="cost-label">Магистратура</span>
                                    <span className="cost-value">{stats.avgCostByType.master.toLocaleString()} ₽</span>
                                </div>
                                <div className="cost-item">
                                    <span className="cost-label">Специалитет</span>
                                    <span className="cost-value">{stats.avgCostByType.specialist.toLocaleString()} ₽</span>
                                </div>
                            </div>
                        </div>

                        <div className="metrics-card">
                            <h3 className="metrics-title">Программы по сферам</h3>
                            <div className="spheres-list">
                                <div className="sphere-item">
                                    <span className="sphere-label">IT и программирование</span>
                                    <span className="sphere-value">{stats.spheres.it.toLocaleString()}</span>
                                </div>
                                <div className="sphere-item">
                                    <span className="sphere-label">Экономика</span>
                                    <span className="sphere-value">{stats.spheres.economics.toLocaleString()}</span>
                                </div>
                                <div className="sphere-item">
                                    <span className="sphere-label">Гуманитарные</span>
                                    <span className="sphere-value">{stats.spheres.humanities.toLocaleString()}</span>
                                </div>
                                <div className="sphere-item">
                                    <span className="sphere-label">Инженерия</span>
                                    <span className="sphere-value">{stats.spheres.engineering.toLocaleString()}</span>
                                </div>
                                <div className="sphere-item">
                                    <span className="sphere-label">Естественные науки</span>
                                    <span className="sphere-value">{stats.spheres.science.toLocaleString()}</span>
                                </div>
                            </div>
                        </div>
        </div>
        <div className="seats-section">
            <h3 className="section-title">Распределение мест по источникам</h3>
            <div className="seats-grid">
                    <div className="seats-card hse">
                        <h4>НИУ ВШЭ</h4>
                        <div className="seats-details">
                            <div className="seat-item">
                                <span className="seat-label">Бюджетные</span>
                                <span className="seat-value budget">{stats.seats.hse.budget.toLocaleString()}</span>
                            </div>
                            <div className="seat-item">
                                <span className="seat-label">Платные</span>
                                <span className="seat-value paid">{stats.seats.hse.paid.toLocaleString()}</span>
                            </div>
                            <div className="seat-item">
                                <span className="seat-label">Для иностранцев</span>
                                <span className="seat-value foreign">{stats.seats.hse.foreign.toLocaleString()}</span>
                            </div>
                        </div>
                    </div>
                <div className="seats-card vuz">
                    <h4>Vuzopedia</h4>
                        <div className="seats-details">
                            <div className="seat-item">
                                <span className="seat-label">Бюджетные</span>
                                <span className="seat-value budget">{stats.seats.vuz.budget.toLocaleString()}</span>
                            </div>
                            <div className="seat-item">
                                <span className="seat-label">Платные</span>
                                <span className="seat-value paid">{stats.seats.vuz.paid.toLocaleString()}</span>
                            </div>
                            <div className="seat-item">
                                <span className="seat-label">Для иностранцев</span>
                                <span className="seat-value foreign">{stats.seats.vuz.foreign.toLocaleString()}</span>
                            </div>
                        </div>
                </div>

            </div>
        </div>

        <div className="career-summary">
            <h3 className="section-title">Карьерные перспективы</h3>
            <div className="career-mini-grid">
                    {stats.careerPaths.slice(0, 3).map((path, index) => (
                        <div key={index} className="career-mini-card">
                            <span className="career-mini-name">{path.name}</span>
                            <span className="career-mini-value">{path.programs.toLocaleString()} прог.</span>
                            <span className="career-mini-salary">{path.avgSalary.toLocaleString()} ₽</span>
                        </div>
                    ))}
                </div>
        </div>
    </div>
    );
}

export default DashboardPage;
