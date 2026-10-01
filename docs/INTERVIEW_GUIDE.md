# Interview Guide

*   **What is CAN and why do embedded systems use it?**
    It's a robust standard for microcontrollers to talk to each other without a host computer.
*   **What is an arbitration ID? Is it the same thing as a signal?**
    No. The ID identifies the frame type and priority. A signal is the data packed inside the frame.
*   **What is a DBC file and what does cantools do with it?**
    A DBC file translates raw bits into engineering values. cantools handles this encoding/decoding.
*   **What is SocketCAN? What is vcan0?**
    SocketCAN is the Linux networking stack for CAN. vcan0 is a virtual CAN interface used for testing.
*   **Why did you use a virtual CAN interface instead of hardware?**
    Because a real ECU wasn't available, and virtual testing enables automated CI workflows.
*   **How do you detect a missing heartbeat?**
    Check the timestamp delta between received frames against a timeout.
*   **Why does the alive counter wrap from 15 to 0?**
    The DBC allocates one byte to the alive counter, but this demo intentionally uses values 0–15 and wraps modulo 16.
*   **Why do timing checks need tolerance?**
    Software timers aren't perfect, especially on non-real-time OSs.
*   **What is the difference between a unit test and an integration/system test in this repository?**
    Unit tests check pure logic like decoding. Integration tests use virtual buses and simulate time.
*   **Why does CI use a virtual backend instead of assuming vcan0?**
    GitHub Actions Ubuntu runners don't expose vcan out of the box without sudo setup.
*   **How would you connect this to a real USB-CAN adapter later?**
    Change `vcan0` to `can0` or the respective adapter channel.
*   **What would need to change to test a real ECU?**
    We would use a physical bus and let the real ECU send the frames instead of `ecu_sim.py`.
*   **What are the major limitations of this project?**
    It's all software-simulated. No physical hardware quirks are tested.
