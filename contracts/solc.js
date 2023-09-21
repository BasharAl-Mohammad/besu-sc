module.exports = {
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
      evmVersion: "byzantium",
      libraries: {
        "@openzeppelin/contracts/utils/math/SafeMath.sol": "0x1234567890abcdef", // Replace with the actual address of SafeMath.sol
        "@openzeppelin/contracts/access/AccessControl.sol": "0x9876543210fedcba", // Replace with the actual address of AccessControl.sol
      },
    },
  };
  