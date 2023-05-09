function doGet(e) {
  const text = LanguageApp.translate(e.parameter.text, e.parameter.src, e.parameter.dest || 'ja')
  return ContentService.createTextOutput(text)
}
