#ifndef L9110HController_h
#define L9110HController_h

class L9110H {
  public:
    L9110H(uint8_t IA, uint8_t IB);
    void initialize();
    void drive(float voltage);
    void stop();

  private:
    uint8_t _IA;
    uint8_t _IB;
    float _voltage;

    float _voltageToPWM(float voltage);
    void _forward(uint8_t PWM);
    void _backward(uint8_t PWM);

};
#endif
