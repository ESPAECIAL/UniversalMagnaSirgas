const IntHayford1924 = require('./IntHayford1924');
const proj4List = require('proj4-list');

describe('IntHayford1924 instantiation', () => {
    it('should not throw an error when instantiated directly', () => {
        let errorCaught;
        try {
            new IntHayford1924();
            errorCaught = false;
        } catch (error) {
            errorCaught = true;
            expect(error.message).toBe("You can instantiate a not abstract class");
        }
        expect(errorCaught).toBe(false);
    });
});

describe('IntHayford1924 integrity', () => {
    const intlHayford1924 = new IntHayford1924();
    const intlHayford1924p = proj4List["EPSG:4022"]
    it('crs should come from PROJ', () => {
        const crsCorrect = [
            intlHayford1924.crs() === intlHayford1924p,
            intlHayford1924.equals(intlHayford1924p)
        ].every(type => type);
        expect(crsCorrect).toBe(true);
    });
    it('boundary coordinates must be numerical', () => {
        const typesCorrect = [
            typeof intlHayford1924.maxNorth() === 'number',
            typeof intlHayford1924.minSouth() === 'number',
            typeof intlHayford1924.maxEast() === 'number',
            typeof intlHayford1924.minWest() === 'number'
        ].every(type => type);
        expect(typesCorrect).toBe(true);
    });
    it('the projection name is incorrect', () => {
        expect(intlHayford1924.nameFromPrj() === 'intl').toBe(true);
    });
    it('the type of the CRS must be ellipsoidal', () => {
        expect(intlHayford1924.crsType() === 'Ellipsoidal').toBe(true);
    });
});