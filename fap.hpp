// LGPL 3 or higher Robert Burner Schadek rburners@gmail.com
#pragma once

#include <fector.hpp>

namespace sweet {

template<typename K, typename V, size_t Size = 128, typename Compare = std::less<K>>
class Fap {
public:
	typedef std::pair<K,V> value_type;
	typedef std::pair<const K,V> const_value_type;
	typedef const_value_type& reference;
	typedef const_value_type& const_reference;
	typedef const_value_type* pointer;
	typedef const const_value_type* const_pointer;
	typedef const_value_type* iterator;
	typedef const const_value_type* const_iterator;

private:
	Compare less;
	static iterator iteratorCast(typename Fector<value_type>::iterator it) {
		return reinterpret_cast<iterator>(it);
	}

	static const_iterator iteratorCast(typename Fector<value_type>::const_iterator it) {
		return reinterpret_cast<const_iterator>(it);
	}

	static pointer pointerCast(typename Fector<value_type>::pointer it) {
		return reinterpret_cast<pointer>(it);
	}

	static const_pointer pointerCast(typename Fector<value_type>::const_pointer it) {
		return reinterpret_cast<const_pointer>(it);
	}

	static reference referenceCast(typename Fector<value_type>::reference it) {
		return reinterpret_cast<reference>(it);
	}

	static const_reference referenceCast(typename Fector<value_type>::const_reference it) {
		return reinterpret_cast<const_reference>(it);
	}

public:

	// insert

	inline std::pair<iterator,bool> insert(const value_type& v) {
		auto it = std::lower_bound(map.begin(), map.end(), v, 
			[&](const std::pair<K,V>& a, const std::pair<K,V>& b) {
				return less(a.first,b.first);
			}
		);

		if(it == this->map.end()) {
			this->map.push_back(v);
			return std::make_pair(iteratorCast(&this->map.back()), true);
		} else if(it->first != v.first) {
			it = this->map.insert(it, v);
			return std::make_pair(iteratorCast(it), true);
		} else {
			return std::make_pair(iteratorCast(it), false);
		}
	}

	// search
	
	inline iterator find(const K& key) {
		auto it = std::lower_bound(map.begin(), map.end(), key, 
			[&](const std::pair<const K,V>& a, const K& b) {
				return less(a.first,b);
			}
		);

		if(it == this->map.end()) {
			return iteratorCast(it);
		} else if(!less(it->first, key)) {
			return iteratorCast(it);
		} else {
			return iteratorCast(this->map.end());
		}
	}

	inline const_iterator find(const K& key) const {
		auto it = std::lower_bound(map.begin(), map.end(), key, 
			[&](const std::pair<K,V>& a, const K& b) {
				return less(a.first,b);
			}
		);

		if(it == this->map.end()) {
			return iteratorCast(it);
		} else if(!less(it->first, key)) {
			return iteratorCast(it);
		} else {
			return iteratorCast(this->map.end());
		}
	}

	// erase
	
	inline size_t erase(const K& key) {
		auto it = this->find(key);
		if(it != this->end()) {
			this->map.erase(it);
			return 1u;
		} else {
			return 0u;
		}
	}

	inline iterator erase(const_iterator it) {
		return iteratorCast(
			this->map.erase(
				reinterpret_cast<value_type*>(const_cast<iterator>(it))
			)
		);
	}

	// iterator

	inline iterator begin() {
		return iteratorCast(this->map.begin());
	}

	inline iterator end() {
		return iteratorCast(this->map.end());
	}

	inline const_iterator begin() const {
		return iteratorCast(this->map.begin());
	}

	inline const_iterator end() const {
		return iteratorCast(this->map.end());
	}

	inline iterator rbegin() {
		return iteratorCast(this->map.rbegin());
	}

	inline iterator rend() {
		return iteratorCast(this->map.rend());
	}

	inline const_iterator rbegin() const {
		return iteratorCast(this->map.rbegin());
	}

	inline const_iterator rend() const {
		return iteratorCast(this->map.rend());
	}

	inline size_t size() const noexcept {
		return this->map.size();
	}

private:
	Fector<value_type, Size> map;
};


} // namespace sweet
