import Api from '~/shared/Api';

export default class extends Api {
  constructor() {
    super('/api/address-normalization');
  }

  async addressNormalization(address) {
    return this.client.post('/', {address});
  }
}