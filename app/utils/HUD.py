import cv2


class HUD:

    def draw(self, frame, analytics, events):

        overlay = frame.copy()

        # -----------------------------
        # Background Panel
        # -----------------------------

        cv2.rectangle(
            overlay,
            (10, 10),
            (360, 250),
            (40, 40, 40),
            -1,
        )

        alpha = 0.55

        frame = cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1 - alpha,
            0,
        )

        white = (255, 255, 255)

        green = (0, 255, 0)

        yellow = (0, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX

        x = 25
        y = 40

        line = 30

        # -----------------------------
        # Title
        # -----------------------------

        cv2.putText(
            frame,
            "AI Vision Intelligence Platform",
            (x, y),
            font,
            0.7,
            green,
            2,
        )

        y += line * 2

        # -----------------------------
        # Statistics
        # -----------------------------

        stats = [

            ("FPS", analytics.fps),

            ("Current Vehicles", analytics.current_vehicle_count),

            ("Unique Vehicles", analytics.unique_vehicle_count),

            ("Traffic Density", analytics.traffic_density),

            ("Congestion", analytics.congestion_level),

        ]

        for title, value in stats:

            value_color = yellow

            if title == "Congestion":

                if value == "FREE FLOW":
                    value_color = (0, 255, 0)

                elif value == "MODERATE":
                    value_color = (0, 255, 255)

                elif value == "HEAVY":
                    value_color = (0, 165, 255)

                else:
                    value_color = (0, 0, 255)

            cv2.putText(
                frame,
                title,
                (x, y),
                font,
                0.6,
                white,
                2,
            )

            cv2.putText(
                frame,
                str(value),
                (250, y),
                font,
                0.6,
                value_color,
                2,
            )

            y += line

        # -----------------------------
        # Vehicle Counts
        # -----------------------------

        for vehicle, count in analytics.vehicle_count.items():

            cv2.putText(
                frame,
                vehicle.capitalize(),
                (x, y),
                font,
                0.55,
                white,
                2,
            )

            cv2.putText(
                frame,
                str(count),
                (250, y),
                font,
                0.55,
                green,
                2,
            )

            y += line
        # -----------------------------
        # Events
        # -----------------------------

        if events:

            y += 20

            cv2.line(
                frame,
                (20, y),
                (340, y),
                (100, 100, 100),
                1,
            )

            y += 30

            cv2.putText(
                frame,
                "Events",
                (x, y),
                font,
                0.6,
                white,
                2,
            )

            y += 30

            for event in events:

                if event.severity == "HIGH":
                    color = (0, 0, 255)

                elif event.severity == "MEDIUM":
                    color = (0, 165, 255)

                else:
                    color = (0, 255, 0)

                cv2.putText(
                    frame,
                    event.title,
                    (x, y),
                    font,
                    0.55,
                    color,
                    2,
                )

                y += 25
        return frame