import Api from '~/shared/Api';

export default class extends Api {
  /**
   * Initialize the API client.
   */
  constructor() {
    super('/api/minor-check');
  }

  /**
   * Check minor.
   */
  async minorCheck(type, dataUrl) {
    return this.client.post('/', {type, image: dataUrl});
  }
}