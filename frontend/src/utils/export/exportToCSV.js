export const exportToCSV = (dataToExport) => {
    if (!dataToExport.programs || dataToExport.programs.length === 0) {
        return null;
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
            escapeCSV(p.name || ''),
            escapeCSV(p.code || ''),
            p.cost ? p.cost.toLocaleString() : '',
            escapeCSV(p.study_type || ''),
            p.budget_places || '0',
            p.paid_places || '0',
            p.foreigners_places || '0',
             escapeCSV('НИУ ВШЭ')
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
            escapeCSV(p.name || ''),
            escapeCSV(p.code || ''),
            p.cost ? p.cost.toLocaleString() : '',
            escapeCSV(p.study_type || ''),
            escapeCSV(p.sphere || ''),
            escapeCSV(p.career_prospects || ''),
            p.min_budget_score || '',
            p.min_paid_score || '',
            escapeCSV('Vuzopedia')
        ]);
    } else {
        throw new Error("Неверный источник данных!")
    }


    const csvContent = [
        headers.join(';'),
        ...rows.map(row => row.join(';'))
    ].join('\n');

    return new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' });
}

const escapeCSV = (str) => {
    if (!str) return '';
    const stringValue = String(str);
    if (stringValue.includes(',') ||
        stringValue.includes('"') ||
        stringValue.includes('\n') ||
        stringValue.includes(';')) {
        return `"${stringValue.replace(/"/g, '""')}"`;
    }
    return stringValue;
};
