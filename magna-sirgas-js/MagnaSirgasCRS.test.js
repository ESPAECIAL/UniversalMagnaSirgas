const MagnaSirgasCRS = require('./MagnaSirgasCRS');

describe('MagnaSirgasCRS', () => {
    it('should throw an error when instantiated directly', () => {
        let errorCaught;
        try {
            new MagnaSirgasCRS();
            errorCaught = false;
        } catch (error) {
            errorCaught = true;
            expect(error.message).toBe("You can't instantiate an abstract class");
        }
        expect(errorCaught).toBe(true);
    });
});
