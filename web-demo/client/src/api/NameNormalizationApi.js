import Api from '~/shared/Api';

export default class extends Api {
  constructor() {
    super('/api/name-normalization');
  }

  async nameNormalization(name) {
    return this.client.post('/', {name});
  }
}