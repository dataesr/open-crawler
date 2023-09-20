export function timeBetween(startDate: Date, endDate: Date) {
  if (!startDate || !endDate) return 'date invalide';
  const ms = endDate.valueOf() - startDate.valueOf();
  const seconds = (ms / 1000);
  const minutes = (ms / (1000 * 60));
  const hours = (ms / (1000 * 60 * 60));
  const days = (ms / (1000 * 60 * 60 * 24));
  if (seconds < 60) return `${seconds.toFixed(0)}s`;
  if (minutes < 60) return `${minutes.toFixed(1)}m`;
  if (hours < 24) return `${hours.toFixed(1)}h`;
  return `${days.toFixed(1)}d`;
}

function time(date: Date) {
  if (!date) return 'date invalide';
  const seconds = Math.abs(Math.floor((new Date().valueOf() - date.valueOf()) / 1000));
  let interval = seconds / 31536000;
  if (interval > 1) {
    return `${Math.floor(interval)} ans`;
  }
  interval = seconds / 2592000;
  if (interval > 1) {
    return `${Math.floor(interval)} mois`;
  }
  interval = seconds / 86400;
  if (interval > 1) {
    return `${Math.floor(interval)} jours`;
  }
  interval = seconds / 3600;
  if (interval > 1) {
    return `${Math.floor(interval)} heures`;
  }
  interval = seconds / 60;
  if (interval > 1) {
    return `${Math.floor(interval)} minutes`;
  }
  return `${Math.floor(seconds)} secondes`;
}

export function timeSince(date: Date) {
  if (!date) return 'date invalide';
  return time(date);
}

export function timeTo(date: Date) {
  if (!date) return 'date invalide';
  return time(date);
}
