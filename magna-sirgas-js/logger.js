const winston = require('winston');

// Create a logger instance
const logger = winston.createLogger({
    level: 'info', // Set the default logging level
    format: winston.format.json(), // Choose a log format (optional)
    transports: [
        new winston.transports.Console(), // Log to the console
        new winston.transports.File({ filename: 'logfile.log' }) // Log to a file
    ]
});

module.exports = logger;
