import { exportToJSON } from './exportToJSON';
import { formatFileName, prepareExportData } from './formatters';
import { exportToCSV } from './exportToCSV';
import { exportToXLSX } from './exportToXLSX';
import { exportToPDF } from './exportToPDF';

const exporters = {
  json: exportToJSON,
  csv: exportToCSV,
  xlsx: exportToXLSX,
  pdf: exportToPDF,
};
export const exportPrograms = (programs, source, filters, totalPrograms, format) => {
  if (!programs || programs.length === 0) {
    throw new Error('Нет данных для экспорта');
  }

  const data = prepareExportData(programs, source, filters, totalPrograms);

  const exporter = exporters[format];
  if (!exporter) {
    throw new Error(`Неподдерживаемый формат: ${format}`);
  }

  const blob = exporter(data);
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;

  link.download = formatFileName(source, format);

  link.click();
  URL.revokeObjectURL(url);
  return true;
};
