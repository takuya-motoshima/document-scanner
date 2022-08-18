import axios from 'axios';

/**
 * REST client.
 */
export default class {
  /**
   * Construct REST client.
   */
  constructor(path, host = undefined) {
    // Client instance.
    const baseURL = `${host || location.origin}/${path.replace(/^\//, '')}`;
    this.client = axios.create({
      baseURL,
      // baseURL: `${host || location.origin}/api/${path.replace(/^\//, '')}`,
      timeout: 60000,
      // timeout: 5000,
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        // 'X-Requested-With': 'XMLHttpRequest'
      },
      responseType: 'json',
      // transformRequest: [
      //   (data, headers) => {
      //     return data;
      //   }
      // ],
      withCredentials: true,
      onUploadProgress: evnt => {
        const percentCompleted = Math.round((evnt.loaded * 100) / evnt.total);
        if (this.uploadProgressHandler)
          this.uploadProgressHandler(percentCompleted);
      }
    });

    // Hook before sending a request.
    this.client.interceptors.request.use(config => {
      // if (config.data instanceof FormData)
      //   config.headers['Content-Type'] = 'multipart/form-data';
      return config;
    });

    // File upload progress event handler.
    this.uploadProgressHandler = undefined;
  }

  /**
   * Tracking file upload progress.
   */
  onUploadProgress(handler = percentCompleted => {}) {
    this.uploadProgressHandler = handler;
  }
}