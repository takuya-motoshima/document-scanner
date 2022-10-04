import Api from '~/shared/Api';

export default class extends Api {
  constructor() {
    super('/api/minor-check');
  }

  async minorCheck(type, dataUrl) {
    return this.client.post('/', {type, image: dataUrl});
  }
}