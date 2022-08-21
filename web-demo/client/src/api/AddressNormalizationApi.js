import Api from '~/shared/Api';

export default class extends Api {
  /**
   * Initialize the API client.
   */
  constructor() {
    super('/api/address-normalization');
  }

  /**
   * Normalized address.
   */
  async addressNormalization(address) {
    return this.client.post('/', {address});
  }
}