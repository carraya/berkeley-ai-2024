export function convertTimestamp(timestamp) {
    var date = new Date(timestamp * 1000); // Convert to milliseconds
    var options = { month: 'long', day: 'numeric', year: 'numeric' };
    var formattedDate = date.toLocaleDateString('en-US', options);
    return formattedDate;
  }

export function ago(timestamp) {
  // Function to convert timestamp to time ago (Display in Seconds, Minutes, Hours, Days, Weeks, Months, Years, etc)
  const time = new Date(timestamp * 1000);
  const now = new Date();
  const diff = now - time;
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) {
    return seconds + " Second" + (seconds === 1 ? "" : "s") + " Ago";
  }
  else if (minutes < 60) {
    return minutes + " Minute" + (minutes === 1 ? "" : "s") + " Ago";
  }
  else if (hours < 24) {
    return hours + " Hour" + (hours === 1 ? "" : "s") + " Ago";
  }
  else if (days < 7) {
    return days + " Day" + (days === 1 ? "" : "s") + " Ago";
  }
  else if (days < 30) {
    return Math.floor(days / 7) + " Week" + (Math.floor(days / 7) === 1 ? "" : "s") + " Ago";
  }
  else if (days < 365) {
    return Math.floor(days / 30) + " Month" + (Math.floor(days / 30) === 1 ? "" : "s") + " Ago";
  }
  else if (days >= 365) {
    return Math.floor(days / 365) + " Year" + (Math.floor(days / 365) === 1 ? "" : "s") + " Ago";
  }
  else {
    return "Unknown Time Ago";
  }
}
