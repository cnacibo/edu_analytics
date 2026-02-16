import * as XLSX from 'xlsx';
export const exportToXLSX = (dataToExport) => {
    const wb = XLSX.utils.book_new();
    const mainData = [
        ['Образовательные программы', dataToExport.source],
        ['Дата экспорта:', dataToExport.exportDate],
        ['Всего программ:', dataToExport.totalPrograms],
        []
    ];
    if (dataToExport.filters && Object.keys(dataToExport.filters).length > 0) {
        mainData.push(['Примененные фильтры:']);
        Object.entries(dataToExport.filters)
            .filter(([_, v]) => v)
            .forEach(([k, v]) => {
                mainData.push([k, v]);
            });
        mainData.push([]);
    }

    let headers = [];
    let rows = [];

    if (dataToExport.source === "hse") {
         headers = [
            'Название',
            'Код',
            'Стоимость (₽/год)',
            'Тип обучения',
            'Бюджетные места',
            'Платные места',
            'Места для иностранцев',
            'Источник',
        ];
        rows = dataToExport.programs.map(p => [
            p.name || '',
            p.code || '',
            p.cost ? p.cost.toLocaleString() + ' ₽' : '',
            p.study_type || '',
            p.budget_places || '0',
            p.paid_places || '0',
            p.foreigners_places || '0',
            'НИУ ВШЭ'
        ]);
    } else if (dataToExport.source === "vuz") {
        headers = [
            'Название',
            'Код',
            'Стоимость (₽/год)',
            'Тип обучения',
            'Сфера',
            'Карьерные перспективы',
            'Мин. балл (бюджет)',
            'Мин. балл (платное)',
            'Источник',
        ];
        rows = dataToExport.programs.map(p => [
            p.name || '',
            p.code || '',
            p.cost ? p.cost.toLocaleString() + ' ₽' : '',
            p.study_type || '',
            p.sphere || '',
            p.career_prospects || '',
            p.min_budget_score || '',
            p.min_paid_score || '',
            'Vuzopedia'
        ]);
    } else {
        throw new Error("Неверный источник данных!")
    }

    mainData.push(headers);
    mainData.push(...rows);

    const ws = XLSX.utils.aoa_to_sheet(mainData);


     XLSX.utils.book_append_sheet(wb, ws, 'Programs');
     const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });

    return new Blob([wbout], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
};
