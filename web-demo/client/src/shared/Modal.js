// import hbs from 'handlebars-extd';
import * as utils from '~/shared/utils';

/**
 * base class of modal.
 */
export default class {
  /**
   * construct modal.
   */
  constructor() {
    this.node;
    this.instance;
    this.resolve;
    this.res = false;
  }

  /**
   * Show Modal.
   */
  async show(...params) {
    // Modal initialization.
    if (utils.isAsyncFunction(this.initialization))
      [this.node, this.instance] = await this.initialization.apply(this, params);
    else 
      [this.node, this.instance] = this.initialization.apply(this, params);

    // When the modal is closed, return a response and then dispose this modal.
    this.node.on('hidden.bs.modal', () => {
      this.resolve(this.res);
      this.dispose();
    });

    // Initialize response.
    this.res = false;

    // Show Modal.
    this.instance.show();

    // Return Promise to Client.
    return new Promise(resolve => this.resolve = resolve);
  }

  /**
   * Modal initialization.
   * Must be implemented in a subclass.
   */
  async initialization() {}

  /**
   * Dispose Modal.
   */
  dispose() {
    this.instance.dispose();
    this.node.remove();
  }

  /**
   * Hide Modal.
   */
  hide(res = undefined) {
    if (res !== undefined)
      this.res = res;
    this.instance.hide();
  }
}