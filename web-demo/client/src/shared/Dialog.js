import fusion from 'deep-fusion';

/**
 * Display various dialogs.
 */
export default class {
  /**
   * Show confirm.
   */
  static async confirm(text, options = null) {
    // Initialize options.
    options = fusion({
      icon: 'question',
      confirmButtonText: 'OK',
      cancelButtonText: '取り消し',
      customClass: {
        confirmButton: `btn fw-bolder btn-primary`,
        cancelButton: 'btn fw-bolder btn-active-light-primary'
      }
    }, options);

    // Show the dialog.
    return (await Swal.fire({
      html: text,
      showCancelButton: true,
      buttonsStyling: false,
      ...options
    })).isConfirmed;
  }

  /**
   * Show success.
   */
  static async success(text, title = null, options = null) {
    // Initialize options.
    options = fusion({
      confirmButtonText: 'OK',
      customClass: {
        confirmButton: `btn fw-bolder btn-primary`,
      }
    }, options);

    // Show the dialog.
    return Swal.fire({
      html: text,
      title,
      icon: 'success',
      buttonsStyling: false,
      ...options
    });
  }

  /**
   * Show error.
   */
  static async error(text, title = null, options = null) {
    // Initialize options.
    options = fusion({
      confirmButtonText: 'OK',
    }, options);

    // Show the dialog.
    return Swal.fire({
      text,
      title,
      icon: 'error',
      buttonsStyling: false,
      customClass: {
        confirmButton: `btn fw-bolder btn-danger`,
      },
      ...options
    });
  }

  /**
   * Show warning.
   */
  static async warning(text, title = null, options) {
    // Initialize options.
    options = fusion({
      confirmButtonText: 'OK'
    }, options);

    // Show the dialog.
    return Swal.fire({
      html: text,
      title,
      icon: 'warning',
      buttonsStyling: false,
      customClass: {
        confirmButton: `btn fw-bolder btn-warning`,
      },
      ...options
    });
  }

  /**
   * Show info.
   */
  static async info(text, title = null, options) {
    // Initialize options.
    options = fusion({
      confirmButtonText: 'OK'
    }, options);

    // Show the dialog.
    return Swal.fire({
      html: text,
      title,
      icon: 'info',
      buttonsStyling: false,
      customClass: {
        confirmButton: `btn fw-bolder btn-primary`,
      },
      ...options
    });
  }

  /**
   * Show unknown error.
   */
  static async unknownError() {
    return this.error(
      'エラーが発生したため処理を中断しました。再度お試しください。何度も発生する場合は、お問い合わせ窓口までご連絡ください。',
      '予期せぬエラーが発生しました。'
    );
  }

  /**
   * Show loading.
   */
  static async loading(text, title = null, options) {
    // Show the dialog.
    return Swal.fire({
      html: text,
      title,
      allowEscapeKey: false,
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading()
      }
    });
  }

  /**
   * Close.
   */
  static close() {
    Swal.close();
  }
}