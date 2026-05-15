from app.scheduler.pipeline_scheduler import (
    PipelineScheduler
)


def main():

    scheduler = PipelineScheduler()

    scheduler.start()


if __name__ == "__main__":
    main()