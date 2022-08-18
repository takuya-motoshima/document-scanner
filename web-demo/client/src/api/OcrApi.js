import Api from '~/shared/Api';

export default class extends Api {
  /**
   * Initialize the API client.
   */
  constructor() {
    super('/api/ocr');
  }

  /**
   * Perform OCR.
   */
  async ocr(type, dataUrl) {
    return this.client.post('/', {type, image: dataUrl});
  }
}