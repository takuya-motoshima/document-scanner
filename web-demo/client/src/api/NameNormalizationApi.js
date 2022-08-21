import Api from '~/shared/Api';

export default class extends Api {
  /**
   * Initialize the API client.
   */
  constructor() {
    super('/api/name-normalization');
  }

  /**
   * Name normalization.
   */
  async nameNormalization(name) {
    return this.client.post('/', {name});
  }
}