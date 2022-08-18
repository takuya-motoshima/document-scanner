import hbs from 'handlebars-extd';

/**
 * Toast display.
 * @example
 *
 * import Toast from '~/shared/Toast';
 * 
 * // Show success message.
 * Toast.success('This is a toast message');
 * 
 * // Show info messages.
 * Toast.info('This is a toast message');
 * 
 * // Show error message.
 * Toast.error('This is a toast message');
 * 
 * // Show warning message.
 * Toast.warning('This is a toast message');
 */
export default class {
  /**
   * Show success message.
   *
   * @param {string}  message Display text.
   * @param {number}  delay   The number of milliseconds until it is automatically hidden.
   */
  static success(message, delay = 5000) {
    this.show(message, 'success', delay);
  }

  /**
   * Show info message.
   *
   * @param {string}  message Display text.
   * @param {number}  delay   The number of milliseconds until it is automatically hidden.
   */
  static info(message, delay = 5000) {
    this.show(message, 'info', delay);
  }

  /**
   * Show warning message.
   *
   * @param {string}  message Display text.
   * @param {number}  delay   The number of milliseconds until it is automatically hidden.
   */
  static warning(message, delay = 5000) {
    this.show(message, 'warning', delay);
  }

  /**
   * Show error message.
   *
   * @param {string}  message Display text.
   * @param {number}  delay   The number of milliseconds until it is automatically hidden.
   */
  static error(message, delay = 5000) {
    this.show(message, 'error', delay);
  }

  /**
   * Show toast.
   *
   * @param {string}                      message Display text.
   * @param {success|info|warning|error}  type    Toast type.
   * @param {number}                      delay   The number of milliseconds until it is automatically hidden.
   */
  static async show(message, type = 'success', delay = 5000) {
    // Add a wrapper element that surrounds the toasts.
    let container = $('.toast-container');
    if (!container.length)
      // Create container element.
      container = $('<div />', {
        class: 'toast-container position-fixed bottom-0 start-0 p-3',
        style: 'z-index: 1080;'
      }).appendTo('body');

    // Current time.
    const now = moment().format('HH:mm:ss');

    // Create new toast element.
    const toastNode = $(hbs.compile(
      `<div class="toast toast-{{type}} bg-body" role="alert" aria-live="assertive" aria-atomic="true" style="box-shadow: 0px 0px 30px rgb(0 0 0 / 30%);">
        <div class="toast-header bg-body text-gray-700" style="border-color: var(--bs-gray-200);">
          {{#if (eq type 'success')}}
            <i class="fas fa-check fs-2 text-success me-3"></i>
            <strong class="me-auto">成功</strong>
          {{else if (eq type 'info')}}
            <i class="fas fa-info fs-2 text-info me-3"></i>
            <strong class="me-auto">情報</strong>
          {{else if (eq type 'warning')}}
            <i class="fas fa-exclamation-triangle fs-2 text-warning me-3"></i>
            <strong class="me-auto">警告</strong>
          {{else}}
            <i class="fas fa-times fs-2 text-danger me-3"></i>
            <strong class="me-auto">エラー</strong>
          {{/if}}
          <small>{{now}}</small>
          <div class="btn btn-sm btn-icon btn-active-color-primary" data-bs-dismiss="toast" aria-label="Close" style="transform: translate(25%, -25%);">
            <!--begin::Svg Icon | path: icons/duotune/arrows/arr061.svg-->
            <span class="svg-icon svg-icon-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect opacity="0.5" x="6" y="17.3137" width="16" height="2" rx="1" transform="rotate(-45 6 17.3137)" fill="currentColor"></rect>
                <rect x="7.41422" y="6" width="16" height="2" rx="1" transform="rotate(45 7.41422 6)" fill="currentColor"></rect>
            </svg></span>
            <!--end::Svg Icon-->
          </div>
        </div>
        <div class="toast-body">{{message}}</div>
      </div>`)({message, type, now})).appendTo(container);

    // Create new toast instance.
    const toast = new bootstrap.Toast(toastNode.get(0), {autohide: delay > 0, delay});

    // Sound a notification sound.
    if (!this.notifSound)
      this.notifSound = new Audio('/build/media/sounds/ding.mp3');   

    // If audio is played while the document has never been clicked, an error will occur, so handling the error will ensure that the process is not interrupted.
    try {
      this.notifSound.pause();
      this.notifSound.currentTime = 0;
      await this.notifSound.play();
    } catch {}
    
    // Toggle toast to show.
    toast.show();

    // Delete the element when you close the toast.
    toastNode.on('hidden.bs.toast', evnt => {
      $(evnt.currentTarget).remove();

      // Delete the container if there is no toast element.
      if (!container.find('.toast').length)
        container.remove();
    });
  }
}