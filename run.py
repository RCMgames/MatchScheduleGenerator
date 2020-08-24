from ScheduleGenerator import ScheduleGenerator

generator = ScheduleGenerator(False)
generator.init_parameters()
generator.find_optimal_schedule()
generator.write_schedule()