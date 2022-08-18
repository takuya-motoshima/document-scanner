/**
 * Return elements with data-ref attribute.
 */
export default (context = 'body', originalRef = undefined, additionalNodeRef = undefined) => {
  // Check parameters.
  if($.type(context) === 'string' || context instanceof HTMLElement)
    context = $(context);
  else if (!(context instanceof $))
    throw new TypeError('The context parameter is invalid');

  // By way of.
  if (originalRef && additionalNodeRef)
    // Add new elements to existing references.
    originalRef[additionalNodeRef] = context.find(`[data-ref="${additionalNodeRef}"]`);
  else {
    // Generate a new reference.
    // Find elements with data-ref attribute.
    const reference = {};
    context.find('[data-ref]').each((_, elem) => {
      const key = elem.dataset.ref;
      if (key in reference)
        reference[key] = reference[key].add($(elem));
      else
        reference[key] = $(elem);
    });
    return reference;
  }
}