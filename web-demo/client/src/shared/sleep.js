/**
 * Delay execution.
 */
export default async milliSeconds => {
  return new Promise(rslv => setTimeout(rslv, milliSeconds));
}