#include <decimal.hpp>
#include <unit.hpp>

UNITTEST(decimal1_test) {
	sweet::Decimal d;

	auto d1(d + 1);
	auto d2(d + 1.0);

	d1 += 2;
	std::cout<<d<<std::endl;
	std::cout<<d1<<std::endl;
	std::cout<<d2<<std::endl;
	sweet::Decimal d3(0.1);
	std::cout<<d3<<std::endl;

	ASSERT_T_C(d1 > d3, [&](){
		LOG("%s > %s", d1,d2);
	});
	d1 = d3;
	ASSERT_EQ(d1,d3);
	std::cout<<d1<<std::endl;
	d1 = d1 * d3;
}

UNITTEST(decimal2minus) {
	sweet::Decimal d(1.0);

	std::cout<<"\n"<<d<<std::endl;
	auto d2 = d - sweet::Decimal(1.1);
	std::cout<<d2<<std::endl;
}
