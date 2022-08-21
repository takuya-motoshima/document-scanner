import Api from '~/shared/Api';

export default class extends Api {
  /**
   * Initialize the API client.
   */
  constructor() {
    super('/api/address-normalization');
  }

  /**
   * Address normalization.
   */
  async addressNormalization(address) {
    return this.client.post('/', {address});
  }
}