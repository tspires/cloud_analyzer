import {defineStore} from 'pinia'
import {useLocalStorage} from '@vueuse/core'
import {toggleDocumentAttribute} from '@/helpers'

type LayoutType = {
    theme: 'light' | 'dark'
    topBarColor: 'light' | 'dark'
    leftSideBarColor: 'light' | 'dark'
    leftSideBarSize: 'sm-hover-active' | 'sm-hover' | 'hidden' | 'condensed' | 'default'
}

const defaultConfig: LayoutType = {
    theme: 'light',
    topBarColor: 'light',
    leftSideBarColor: 'dark',
    leftSideBarSize: 'sm-hover-active'
}

export const useLayoutStore = defineStore('layout_store', () => {
    const layout = useLocalStorage<LayoutType>('rasket_layout_store', defaultConfig)

    const setTheme = (nTheme: LayoutType['theme']) => {
        layout.value.theme = nTheme
        toggleDocumentAttribute('data-bs-theme', layout.value.theme)
    }

    const setTopBarColor = (nColor: LayoutType['topBarColor']) => {
        layout.value.topBarColor = nColor
        toggleDocumentAttribute('data-topbar-color', layout.value.topBarColor)
    }

    const setLeftSideBarColor = (nColor: LayoutType['leftSideBarColor']) => {
        layout.value.leftSideBarColor = nColor
        toggleDocumentAttribute('data-menu-color', layout.value.leftSideBarColor)
    }

    const setLeftSideBarSize = (nSize: LayoutType['leftSideBarSize']) => {
        layout.value.leftSideBarSize = nSize
        toggleDocumentAttribute('data-menu-size', layout.value.leftSideBarSize)
    }

    const reset = () => {
        setTheme(defaultConfig.theme)
        setTopBarColor(defaultConfig.topBarColor)
        setLeftSideBarColor(defaultConfig.leftSideBarColor)
        setLeftSideBarSize(defaultConfig.leftSideBarSize)
    }

    const init = () => {
        setTheme(layout.value.theme)
        setTopBarColor(layout.value.topBarColor)
        setLeftSideBarColor(layout.value.leftSideBarColor)
        setLeftSideBarSize(layout.value.leftSideBarSize)
    }

    return {
        layout,
        setTheme,
        setTopBarColor,
        setLeftSideBarColor,
        setLeftSideBarSize,
        reset,
        init
    }
})
