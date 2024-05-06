const EllipsoidalCRS = require('./EllipsoidalCRS');

describe('EllipsoidalCRS', () => {
    it('should not throw an error when instantiated directly', () => {
        let errorCaught;
        try {
            errorCaught = false;
            new EllipsoidalCRS();
        } catch (error) {
            errorCaught = true;
            expect(error.message).toBe("You can instantiate a not abstract class");
        }
        expect(errorCaught).toBe(false);
    });
});
