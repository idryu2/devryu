import { useState } from 'react'
import './header.css'

export default function Header() {
  const [query, setQuery] = useState('')

  const handleSearch = (e) => {
    e.preventDefault()
    const q = query.trim()
    if (!q) return
    // 실제 네이버 통합검색으로 보낸다. (데모용)
    window.open(
      `https://search.naver.com/search.naver?query=${encodeURIComponent(q)}`,
      '_blank',
      'noopener',
    )
  }

  return (
    <header className="header">
      <div className="container header__inner">
        <a className="logo" href="/" aria-label="NAVER 홈">
          NAVER
        </a>

        <form className="gnb-search" onSubmit={handleSearch} role="search">
          <input
            className="gnb-search__input"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="검색어를 입력해 주세요."
            aria-label="통합 검색"
          />
          <button className="gnb-search__btn" type="submit" aria-label="검색">
            🔍
          </button>
        </form>

        <nav className="gnb-links" aria-label="주요 메뉴">
          <a href="#blog">블로그</a>
          <a href="#" >메일</a>
          <a href="#" >카페</a>
        </nav>
      </div>
    </header>
  )
}
