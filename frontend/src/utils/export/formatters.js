export const formatDate = (date = new Date()) => {
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatFileName = (source, format) => {
  const date = new Date().toISOString().slice(0, 10);
  return `programs_${source}_${date}.${format}`;
};

export const prepareExportData = (programs, source, filters, total) => ({
  programs,
  source,
  filters,
  exportDate: formatDate(),
  totalPrograms: total,
});
