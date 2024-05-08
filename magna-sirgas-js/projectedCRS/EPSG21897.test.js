const EPSG21897 = require('./EPSG21897');
const proj4List = require('proj4-list');

describe('EPSG21897 instantiation', () => {
    var errorCaught;
    it('should not throw an error when instantiated directly', () => {
        try {
            new EPSG21897();
            errorCaught = false;
        } catch (error) {
            errorCaught = true;
            expect(error.message).toBe("You can instantiate a not abstract class");
        }
        expect(errorCaught).toBe(false);
    });
});

describe('EPSG21897 integrity', () => {
    const epsg21897 = new EPSG21897();
    const epsg21897p = proj4List["EPSG:21897"]
    it('crs should come from PROJ', () => {
        const crsCorrect = [
            epsg21897.crs() === epsg21897p,
            epsg21897.equals(epsg21897p)
        ].every(type => type);
        expect(crsCorrect).toBe(true);
    });
    it('boundary coordinates must be numerical', () => {
        const typesCorrect = [
            typeof epsg21897.maxNorth() === 'number',
            typeof epsg21897.minSouth() === 'number',
            typeof epsg21897.maxEast() === 'number',
            typeof epsg21897.minWest() === 'number'
        ].every(type => type);
        expect(typesCorrect).toBe(true);
    });
    it('the projection name is incorrect', () => {
        expect(epsg21897.projName() === 'Bogota 1975 / Colombia Bogota zone').toBe(true);
    });
    it('the type of the CRS must be projected', () => {
        expect(epsg21897.crsType() === 'Projected').toBe(true);
    });
});