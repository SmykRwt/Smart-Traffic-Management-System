from app.database.database import SessionLocal

from app.database.models import Analytics


class AnalyticsRepository:

    def save(self, analytics):

        session = SessionLocal()

        try:

            record = Analytics(

                current_vehicle_count=analytics.current_vehicle_count,

                unique_vehicle_count=analytics.unique_vehicle_count,

                traffic_density=analytics.traffic_density,

                congestion_level=analytics.congestion_level,
            )

            session.add(record)

            session.commit()

        finally:

            session.close()