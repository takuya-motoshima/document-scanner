import '~/pages/ocr.css';
import selectAll from '~/shared/selectAll';
import OcrApi from '~/api/OcrApi';
import Dialog from '~/shared/Dialog';
import Scissor from 'js-scissor';

/**
 * Get image as DataURL.
 */
async function getImageAsDataURL() {
  // Width of resizing.
  const resizeWidth = ref.compression.filter(':checked').val();

  // Resize the image.
  if (resizeWidth)
    return (await new Scissor(ref.image.get(0)).resize(parseInt(resizeWidth, 10))).toBase64();

  // Create an empty canvas element.
  const canvas = $('<canvas />').get(0);
  canvas.width = ref.image.get(0).naturalWidth;
  canvas.height = ref.image.get(0).naturalHeight;

  // Copy the image contents to the canvas.
  const ctx = canvas.getContext('2d');
  ctx.drawImage(ref.image.get(0), 0, 0, canvas.width, canvas.height);

  // Get the data-URL formatted image.
  return canvas.toDataURL('image/png', 1);
}

// API.
const ocrApi = new OcrApi();

// Initialize loading indicator.
const blockUI = new KTBlockUI(document.body, {
  message: 
    `<div class="blockui-message text-white">
      <span class="spinner-border text-primary h-20px w-20px me-2"></span>
      <span id="uploadProgress" class="fs-3">0</span>%...
    </div>`,
  // message: '<div class="blockui-message fw-bolder"><span class="spinner-border text-primary"></span> Sending...</div>',
  overlayClass: "bg-dark bg-opacity-25"
});

// Find elements.
const ref = selectAll();

// Set event.
ocrApi.onUploadProgress(percentCompleted => {
  $('#uploadProgress').text(percentCompleted);
});
$('body')
  .on('click', '[data-on-ocr]', async () => {
    try {
      // Show loading indicator.
      blockUI.block();

      // Type of identification card to be OCR'd.
      const type = ref.type.filter(':checked').val();

      // Perform OCR.
      const {data} = await ocrApi.ocr(type, await getImageAsDataURL());
      console.log('data=', data);

      // Show the results on the screen.
      if (type === 'driverslicense') {
        ref.driverslicenseFullName.text(data.fullName);
        ref.driverslicenseFirstName.text(data.firstName);
        ref.driverslicenseLastName.text(data.lastName);
        ref.driverslicenseNumber.text(data.licenseNumber);
        ref.driverslicenseExpiryDate.text(data.expiryDate);
        // ref.driverslicenseWesternExpiryDate.text(data.wrnExpiryDate);
        ref.driverslicenseBirthday.text(data.birthday);
        ref.driverslicenseAge.text(data.age ? `${data.age}歳` : '');
        ref.driverslicenseWesternBirthday.text(data.wrnBirthday);
        // ref.driverslicensePostalCode.text(data.postalCode);
        ref.driverslicenseAddress.text(data.address);
      } else {
        ref.mynumberFullName.text(data.fullName);
        ref.mynumberFirstName.text(data.firstName);
        ref.mynumberLastName.text(data.lastName);
        ref.mynumberGender.text(data.gender);
        ref.mynumberCardExpiryDate.text(data.cardExpiryDate);
        // ref.mynumberWesternCardExpiryDate.text(data.wrnCardExpiryDate);
        ref.mynumberDigiExpiryDate.text(data.digiExpiryDate);
        // ref.mynumberWesternDigiExpiryDate.text(data.wrnDigiExpiryDate);
        ref.mynumberBirthday.text(data.birthday);
        ref.mynumberAge.text(data.age ? `${data.age}歳` : '');
        ref.mynumberWesternBirthday.text(data.wrnBirthday);
        // ref.mynumberPostalCode.text(data.postalCode);
        ref.mynumberAddress.text(data.address);
      }

      // Hide the loading indicator.
      blockUI.release();
    } catch (err) {
      // Hide the loading indicator.
      blockUI.release();

      // Show error messages.
      await Dialog.unknownError();
      throw err;
    }
  })
  .on('change', '[data-on-change-type]', () => {
    // Type of identification card to be OCR'd.
    const type = ref.type.filter(':checked').val();

    // After changing the type, set the image to its initial state.
    if (type === 'driverslicense') {
      for (let key of Object.keys(ref))
        if (key.match(/^driverslicense[A-Z][a-zA-Z]+/) && key !== 'driverslicenseOcrResults')
          ref[key].text('');
      ref.driverslicenseOcrResults.removeClass('d-none');
      ref.mynumberOcrResults.addClass('d-none');
      ref.image.attr('src', '/build/media/driverslicense.png');
    } else {
      for (let key of Object.keys(ref))
        if (key.match(/^mynumber[A-Z][a-zA-Z]+/) && key !== 'mynumberOcrResults')
          ref[key].text('');
      ref.driverslicenseOcrResults.addClass('d-none');
      ref.mynumberOcrResults.removeClass('d-none');
      ref.image.attr('src', '/build/media/mynumber.png');
    }
  })
  .on('change', '[data-on-upload-file]', evnt => {
    const reader = new FileReader();
    reader.onload = evnt => ref.image.attr('src', evnt.target.result);
    reader.readAsDataURL(evnt.currentTarget.files[0]);
  });