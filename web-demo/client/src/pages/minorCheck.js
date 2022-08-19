import '~/pages/minorCheck.css';
import selectAll from '~/shared/selectAll';
import MinorCheckApi from '~/api/MinorCheckApi';
import Dialog from '~/shared/Dialog';
import Scissor from 'js-scissor';

/**
 * Get image as DataURL.
 */
async function getImageAsDataURL(resizeWidth = 480) {
  // Resize the image.
  if (resizeWidth)
    return (await new Scissor(ref.image.get(0)).resize(resizeWidth)).toBase64();

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
const minorCheckApi = new MinorCheckApi();

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
minorCheckApi.onUploadProgress(percentCompleted => {
  $('#uploadProgress').text(percentCompleted);
});
$('body')
  .on('click', '[data-on-check]', async () => {
    try {
      // Show loading indicator.
      blockUI.block();

      // Type of identification card to be OCR'd.
      const type = ref.type.filter(':checked').val();

      // Perform OCR.
      const {data} = await minorCheckApi.minorCheck(type, await getImageAsDataURL());
      console.log('data=', data);

      // Hide the loading indicator.
      blockUI.release();

      // Response age to int.
      const age = parseInt(data.age, 10);

      // If the birthdays is not taken, show the error message.
      if (!age)
        return void await Dialog.warning('画像から生年月日を読み取れませんでした');

      // Calculate age.
      if (age >= 20)
        await Dialog.success(null, `年齢は${age}歳で、未成年ではありません`);
      else
        await Dialog.error(null, `年齢は${age}歳で、未成年です`);
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
    if (type === 'driverslicense')
      ref.image.attr('src', '/build/media/driverslicense.png');
    else
      ref.image.attr('src', '/build/media/mynumber.png');
  })
  .on('change', '[data-on-upload-file]', evnt => {
    const reader = new FileReader();
    reader.onload = evnt => ref.image.attr('src', evnt.target.result);
    reader.readAsDataURL(evnt.currentTarget.files[0]);
  });