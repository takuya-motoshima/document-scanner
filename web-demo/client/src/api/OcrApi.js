import Api from '~/shared/Api';

export default class extends Api {
  constructor() {
    super('/api/ocr');
  }

  async ocr(type, dataUrl) {
    return this.client.post('/', {type, image: dataUrl});
  }
}