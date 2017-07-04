# Pixhawk Flight Time

Python script to compute the flight time of a single log or a folder of logs. It takes into account just the time in air, and not the time the Pixhawk was on.

## Prerequisites

None

## Usage

You can use this script in two ways.

To compute the flight time of a single log file, you can use the following command:

```
python flight_time.py -l 'log_filename.log'
```

If you run the script without arguments, it will compute the flight time of all the logs in the folder defined by the constant LOGS_FOLDER_NAME inside the script (by default it's the 'logs' folder used for testing)

```
python flight_time.py
```

## Running the tests

Run the following command

```
python flight_time_tests.py
```

It should analyze the example logs and show the success or failure of them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
