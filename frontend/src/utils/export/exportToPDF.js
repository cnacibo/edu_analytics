import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { loadRoboto } from './fonts/Roboto-Regular-normal';
export const exportToPDF = (dataToExport) => {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'pt',
    format: 'a4',
  });
  loadRoboto(doc);
  doc.setFont('Roboto', 'normal');

  const marginLeft = 14;
  const pageWidth = doc.internal.pageSize.width - marginLeft * 2;
  const lineHeight = 14;

  let yPos = 30;

  doc.setFontSize(20);
  doc.setTextColor(102, 126, 234);
  doc.text('Образовательные программы', marginLeft, yPos);
  yPos += 25;

  doc.setFontSize(12);
  doc.setTextColor(118, 75, 162);
  doc.text(String(dataToExport.source || '').toUpperCase(), marginLeft, yPos);
  yPos += 18;

  doc.setFontSize(10);
  doc.setTextColor(0, 0, 0);

  const exportText = doc.splitTextToSize(`Дата экспорта: ${dataToExport.exportDate}`, pageWidth);
  doc.text(exportText, marginLeft, yPos);
  yPos += exportText.length * lineHeight;

  const totalText = doc.splitTextToSize(
    `Всего программ: ${dataToExport.totalPrograms || 0}`,
    pageWidth
  );
  doc.text(totalText, marginLeft, yPos);
  yPos += totalText.length * lineHeight + 10;

  const filters = dataToExport.filters || {};

  const activeFilters = Object.entries(filters).filter(
    ([_, v]) => v !== null && v !== undefined && String(v).trim() !== ''
  );

  doc.setFontSize(12);
  doc.text('Примененные фильтры:', marginLeft, yPos);
  yPos += 16;

  doc.setFontSize(10);

  if (activeFilters.length === 0) {
    doc.text('нет', marginLeft + 10, yPos);
    yPos += lineHeight + 10;
  } else {
    activeFilters.forEach(([k, v]) => {
      const safeText = `- ${String(k)}: ${String(v)}`;
      const splitFilter = doc.splitTextToSize(safeText, pageWidth - 10);

      doc.text(splitFilter, marginLeft + 10, yPos);
      yPos += splitFilter.length * lineHeight;
    });

    yPos += 10;
  }

  let headers = [];
  let rows = [];

  if (dataToExport.source === 'hse') {
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

    rows = dataToExport.programs.map((p) => [
      p.name || '',
      p.code || '',
      p.cost ? p.cost.toLocaleString() + ' ₽' : '',
      p.study_type || '',
      p.budget_places?.toString() || '0',
      p.paid_places?.toString() || '0',
      p.foreigners_places?.toString() || '0',
      'НИУ ВШЭ',
    ]);
  } else if (dataToExport.source === 'vuz') {
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

    rows = dataToExport.programs.map((p) => [
      p.name || '',
      p.code || '',
      p.cost ? p.cost.toLocaleString() + ' ₽' : '',
      p.study_type || '',
      p.sphere || '',
      p.career_prospects || '',
      p.min_budget_score?.toString() || '',
      p.min_paid_score?.toString() || '',
      'Vuzopedia',
    ]);
  } else {
    throw new Error('Неверный источник данных!');
  }

  autoTable(doc, {
    startY: yPos,
    head: [headers],
    body: rows,
    theme: 'striped',
    styles: {
      font: 'Roboto',
      fontSize: 9,
      cellPadding: 4,
    },
    headStyles: {
      font: 'Roboto',
      fillColor: [102, 126, 234],
      textColor: 255,
      fontStyle: 'normal',
    },
    alternateRowStyles: {
      fillColor: [245, 245, 245],
    },
    margin: { left: marginLeft, right: marginLeft },
    didDrawPage: function (data) {
      const pageNumber = doc.internal.getNumberOfPages();
      doc.setFontSize(8);
      doc.setTextColor(120, 120, 120);
      doc.text(
        `Страница ${pageNumber}`,
        doc.internal.pageSize.width - marginLeft - 30,
        doc.internal.pageSize.height - 10
      );
    },
  });

  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor(120, 120, 120);
    doc.text('Экспортировано из Edu Analytics', marginLeft, doc.internal.pageSize.height - 10);
  }

  return doc.output('blob');
};
