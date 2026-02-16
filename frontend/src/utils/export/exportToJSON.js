export const exportToJSON = (dataToExport) => {
  if (!dataToExport.programs || dataToExport.programs.length === 0) {
    return null;
  }
  const jsonString = JSON.stringify(dataToExport, null, 2);

  return new Blob([jsonString], { type: 'application/json' });
};
