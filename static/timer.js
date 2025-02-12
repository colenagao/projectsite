// Timer settings in seconds
let WORK_TIME = 25 * 60;
let SHORT_BREAK = 5 * 60;
let LONG_BREAK = 15 * 60;
const SESSIONS_BEFORE_LONG_BREAK = 4;

let currentTime = WORK_TIME;
let timerInterval = null;
let isRunning = false;
let sessionCount = 0;
let currentSession = 'Work Session';

// DOM Elements
const timerDisplay = document.getElementById('timer');
const sessionDisplay = document.getElementById('session');
const startButton = document.getElementById('start');
const pauseButton = document.getElementById('pause');
const resetButton = document.getElementById('reset');
const workSessionButton = document.getElementById('work-session');
const shortBreakButton = document.getElementById('short-break');
const longBreakButton = document.getElementById('long-break');
const applySettingsButton = document.getElementById('apply-settings');
const workTimeInput = document.getElementById('work-time');
const shortBreakTimeInput = document.getElementById('short-break-time');
const longBreakTimeInput = document.getElementById('long-break-time');

// Update the display with the current time and session
function updateDisplay() {
    let minutes = Math.floor(currentTime / 60);
    let seconds = currentTime % 60;
    timerDisplay.textContent = 
        `${minutes < 10 ? '0' + minutes : minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
    sessionDisplay.textContent = currentSession;
}

// Start the timer
function startTimer() {
    if (isRunning) return;
    isRunning = true;
    timerInterval = setInterval(() => {
        if (currentTime > 0) {
            currentTime--;
            updateDisplay();
        } else {
            clearInterval(timerInterval);
            isRunning = false;
            handleSessionEnd();
        }
    }, 1000);
}

// Pause the timer
function pauseTimer() {
    if (!isRunning) return;
    clearInterval(timerInterval);
    isRunning = false;
}

// Reset the timer
function resetTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    sessionCount = 0;
    currentSession = 'Work Session';
    currentTime = WORK_TIME;
    updateDisplay();
}

// Handle the end of a session
function handleSessionEnd() {
    if (currentSession === 'Work Session') {
        sessionCount++;
        if (sessionCount % SESSIONS_BEFORE_LONG_BREAK === 0) {
            currentSession = 'Long Break';
            currentTime = LONG_BREAK;
        } else {
            currentSession = 'Short Break';
            currentTime = SHORT_BREAK;
        }
    } else {
        currentSession = 'Work Session';
        currentTime = WORK_TIME;
    }
    updateDisplay();
    startTimer();
}

// Switch to Work Session manually
function switchToWorkSession() {
    clearInterval(timerInterval);
    isRunning = false;
    currentSession = 'Work Session';
    currentTime = WORK_TIME;
    updateDisplay();
}

// Switch to Short Break manually
function switchToShortBreak() {
    clearInterval(timerInterval);
    isRunning = false;
    currentSession = 'Short Break';
    currentTime = SHORT_BREAK;
    updateDisplay();
}

// Switch to Long Break manually
function switchToLongBreak() {
    clearInterval(timerInterval);
    isRunning = false;
    currentSession = 'Long Break';
    currentTime = LONG_BREAK;
    updateDisplay();
}

// Apply user settings for durations
function applySettings() {
    const newWorkTime = parseInt(workTimeInput.value, 10);
    const newShortBreak = parseInt(shortBreakTimeInput.value, 10);
    const newLongBreak = parseInt(longBreakTimeInput.value, 10);

    if (isNaN(newWorkTime) || newWorkTime <= 0) {
        alert('Please enter a valid positive number for Work Time.');
        return;
    }
    if (isNaN(newShortBreak) || newShortBreak <= 0) {
        alert('Please enter a valid positive number for Short Break.');
        return;
    }
    if (isNaN(newLongBreak) || newLongBreak <= 0) {
        alert('Please enter a valid positive number for Long Break.');
        return;
    }

    WORK_TIME = newWorkTime * 60;
    SHORT_BREAK = newShortBreak * 60;
    LONG_BREAK = newLongBreak * 60;

    // If currently in the session being adjusted, update the currentTime
    if (currentSession === 'Work Session') {
        currentTime = WORK_TIME;
    } else if (currentSession === 'Short Break') {
        currentTime = SHORT_BREAK;
    } else if (currentSession === 'Long Break') {
        currentTime = LONG_BREAK;
    }

    updateDisplay();
}

// Event Listeners
startButton.addEventListener('click', startTimer);
pauseButton.addEventListener('click', pauseTimer);
resetButton.addEventListener('click', resetTimer);
workSessionButton.addEventListener('click', switchToWorkSession);
shortBreakButton.addEventListener('click', switchToShortBreak);
longBreakButton.addEventListener('click', switchToLongBreak);
applySettingsButton.addEventListener('click', applySettings);

// Initialize display
updateDisplay();