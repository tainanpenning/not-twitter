export function validateBirthDate(date: string): boolean {
  if (!date) return false;

  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return false;
  }

  const today = new Date();

  if (parsedDate > today) {
    return false;
  }

  const age = today.getFullYear() - parsedDate.getFullYear();

  if (age > 120) {
    return false;
  }

  if (age < 13) {
    return false;
  }

  return true;
}
