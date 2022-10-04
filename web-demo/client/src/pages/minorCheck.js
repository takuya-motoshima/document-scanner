import '~/pages/minorCheck.css';
import selectAll from '~/shared/selectAll';
import MinorCheckApi from '~/api/MinorCheckApi';
import Dialog from '~/shared/Dialog';
import Scissor from 'js-scissor';

async function getImageAsDataURL(resizeWidth = 480) {
  if (resizeWidth)
    return (await new Scissor(ref.image.get(0)).resize(resizeWidth)).toBase64();
  const canvas = $('<canvas />').get(0);
  canvas.width = ref.image.get(0).naturalWidth;
  canvas.height = ref.image.get(0).naturalHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(ref.image.get(0), 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/png', 1);
}

const minorCheckApi = new MinorCheckApi();
const blockUI = new KTBlockUI(document.body, {
  message: 
    `<div class="blockui-message text-white">
      <span class="spinner-border text-primary h-20px w-20px me-2"></span>
      <span id="uploadProgress" class="fs-3">0</span>%...
    </div>`,
  overlayClass: "bg-dark bg-opacity-25"
});

const ref = selectAll();
minorCheckApi.onUploadProgress(percentCompleted => {
  $('#uploadProgress').text(percentCompleted);
});
$('body')
  .on('click', '[data-on-check]', async () => {
    try {
      blockUI.block();
      const type = ref.type.filter(':checked').val();
      const {data} = await minorCheckApi.minorCheck(type, await getImageAsDataURL());
      console.log('data=', data);
      blockUI.release();
      const age = parseInt(data.age, 10);
      if (!age)
        return void await Dialog.warning('画像から生年月日を読み取れませんでした');
      if (age >= 20)
        await Dialog.success(null, `年齢は${age}歳で、未成年ではありません`);
      else
        await Dialog.error(null, `年齢は${age}歳で、未成年です`);
    } catch (err) {
      blockUI.release();
      await Dialog.unknownError();
      throw err;
    }
  })
  .on('change', '[data-on-change-type]', () => {
    const type = ref.type.filter(':checked').val();
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